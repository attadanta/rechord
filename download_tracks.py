from datetime import date, datetime, time, timedelta, timezone
import argparse
from httpx import Client
import os
import time as sys_time
from typing import Generator, Any, Optional
import logging
from dataclasses import dataclass
import json
from last_fm_client import create_authorized_client, create_signed_get_request
from last_fm_model import (
    Method,
    GetRecentTracksInput,
    GetRecentTracksOutput,
    Track,
)


@dataclass
class RecentTracksPage:
    response_body: dict[str, Any]
    tracks: list[Track]
    page: int
    total_pages: int
    elapsed_time: timedelta


def get_recent_tracks_page(
    client: Client,
    secret: str,
    user: str,
    date_from: datetime,
    date_to: datetime,
    page: Optional[int],
) -> RecentTracksPage:
    if page is not None and page < 1:
        raise ValueError("page must be greater than or equal to 1")

    if page is None:
        page = 1

    input = GetRecentTracksInput(
        user=user,
        limit=200,
        page=page,
        date_from=date_from,
        date_to=date_to,
    )

    req = create_signed_get_request(
        client=client,
        secret=secret,
        method=Method.user_get_recent_tracks,
        params=input.as_params(),
    )

    res = client.send(req)
    response_body = res.json()

    recent_tracks_output = GetRecentTracksOutput(**response_body)

    recent_tracks = recent_tracks_output.recent_tracks
    attributes = recent_tracks.attributes
    tracks = recent_tracks.tracks

    return RecentTracksPage(
        tracks=tracks,
        page=attributes.page,
        total_pages=attributes.totalPages,
        elapsed_time=res.elapsed,
        response_body=response_body,
    )


def get_recent_tracks(
    client: Client,
    logger: logging.Logger,
    secret: str,
    user: str,
    date_from: datetime,
    date_to: datetime,
    pause_in_milliseconds: Optional[int] = 1000,
) -> Generator[RecentTracksPage, None, None]:
    if pause_in_milliseconds is not None and pause_in_milliseconds < 0:
        raise ValueError("pause_in_milliseconds must be greater than or equal to 0")

    page = 1

    while True:
        data = get_recent_tracks_page(
            client=client,
            secret=secret,
            user=user,
            date_from=date_from,
            date_to=date_to,
            page=page,
        )
        yield data

        if page >= data.total_pages:
            break

        if pause_in_milliseconds is not None and pause_in_milliseconds > 0:
            logger.debug(
                f"Sleeping for {pause_in_milliseconds} milliseconds before next page",
                extra={"page": page, "total_pages": data.total_pages},
            )
            sys_time.sleep(pause_in_milliseconds / 1000)

        page += 1


def file_name(date_from: datetime, date_to: datetime, page: int) -> str:
    time_format_in_filename = "%Y-%m-%dT%H%M%S"
    return f"tracks_{date_from.strftime(time_format_in_filename)}_{date_to.strftime(time_format_in_filename)}_{str(page).zfill(4)}.json"


def valid_date(s: str) -> date:
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date: {s}")


def main():
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description="Download tracks history from Last.fm."
    )
    parser.add_argument(
        "--api-key",
        help="The API key",
        required=True,
        dest="api_key",
    )
    parser.add_argument("--secret", help="The API secret", required=True, dest="secret")
    parser.add_argument(
        "--session",
        help="The session key for a logged-in user",
        required=True,
        dest="session",
    )
    parser.add_argument(
        "--user",
        help="The username to download tracks for",
        required=True,
        dest="user",
    )
    parser.add_argument(
        "--from",
        help="The start date in the format YYYY-MM-DD",
        required=True,
        dest="date_from",
        type=valid_date,
    )
    parser.add_argument(
        "--to",
        help="The end date in the format YYYY-MM-DD",
        required=True,
        dest="date_to",
        type=valid_date,
    )
    parser.add_argument(
        "--base-url",
        help="The base URL for the Last.fm API",
        required=False,
        dest="base_url",
        default="https://ws.audioscrobbler.com/",
    )
    parser.add_argument(
        "--pause",
        help="The number of milliseconds to pause between requests",
        required=False,
        dest="pause",
        type=int,
        default=1000,
    )
    parser.add_argument(
        "--log-level",
        help="The log level",
        required=False,
        dest="log_level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument(
        "--dest-dir",
        help="The directory to save the downloaded files. Should exist.",
        required=False,
        dest="dest_dir",
        default=".",
    )

    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    api_key = args.api_key
    secret = args.secret
    session_key = args.session
    user = args.user
    base_url = args.base_url
    dest_dir = args.dest_dir

    if not os.path.exists(dest_dir):
        raise ValueError(f"Directory does not exist: {dest_dir}")

    date_from = datetime.combine(args.date_from, time.min, tzinfo=timezone.utc)
    date_to = datetime.combine(args.date_to, time.max, tzinfo=timezone.utc)

    if date_to < date_from:
        raise ValueError("The end date must be greater than or equal to the start date")

    client = create_authorized_client(
        base_url=base_url, api_key=api_key, session_key=session_key
    )

    for p in get_recent_tracks(
        client=client,
        logger=logger,
        secret=secret,
        user=user,
        date_from=date_from,
        date_to=date_to,
    ):
        logger.debug(
            f"Recent tracks page {p.page}/{p.total_pages} took {p.elapsed_time.total_seconds()} seconds"
        )

        dest_file = os.path.join(dest_dir, file_name(date_from, date_to, p.page))

        with open(dest_file, "w") as f:
            f.write(json.dumps(p.response_body))


if __name__ == "__main__":
    main()
