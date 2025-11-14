import asyncio
import json
import os
import tempfile
from unittest.mock import MagicMock

import pytest

from logger import message_handler


@pytest.mark.asyncio
async def test_message_handler_logs_correctly():
    # Create a temporary file for logging
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        log_file = temp_file.name

    try:
        # Mock the message
        msg = MagicMock()
        msg.subject = "test.subject"
        msg.data = b'{"key": "value"}'

        # Call the handler
        await message_handler(msg, log_file)

        # Read the log file
        with open(log_file, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 1
            log_entry = json.loads(lines[0])
            assert log_entry['subject'] == "test.subject"
            assert log_entry['data'] == '{"key": "value"}'
            assert 'timestamp' in log_entry

    finally:
        os.unlink(log_file)


@pytest.mark.asyncio
async def test_message_handler_with_bytes_data():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        log_file = temp_file.name

    try:
        msg = MagicMock()
        msg.subject = "binary.subject"
        msg.data = b'\x00\x01\x02'

        await message_handler(msg, log_file)

        with open(log_file, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 1
            log_entry = json.loads(lines[0])
            assert log_entry['subject'] == "binary.subject"
            assert log_entry['data'] == '\x00\x01\x02'  # decode with replace

    finally:
        os.unlink(log_file)