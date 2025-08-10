"""Process manager for executing hoymiles-mqtt."""

import asyncio
import logging
import signal
import sys
from collections.abc import Mapping
from typing import Any

from .const import NO_CONFIG_VALUE

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ProcessManager:
    """A class to manage a single subprocess using asyncio."""

    def __init__(self, command: list[str]) -> None:
        """
        Initialize the ProcessManager.

        Args:
            command: A list of strings representing the command and its arguments.

        """
        self.command = command
        self._process = None

    async def start_process(self) -> None:
        """
        Start the subprocess asynchronously.

        This method creates and runs the subprocess. It waits for the process
        to start and stores a reference to it.
        """
        if self._process is not None:
            _LOGGER.debug("Process is already running.")
            return

        _LOGGER.debug("Starting process: %s", " ".join(self.command))
        self._process = await asyncio.create_subprocess_exec(
            *self.command, stdout=sys.stdout, stderr=sys.stderr
        )
        _LOGGER.debug("Process started with PID: %s", self._process.pid)

    async def terminate_process(self) -> None:
        """
        Terminate the subprocess gracefully if it's running.

        This method attempts a graceful shutdown first using SIGINT (Ctrl+C).
        If the process does not terminate within a timeout, it sends a SIGTERM.
        If it's still running after another timeout, it sends a SIGKILL
        to force termination.
        """
        if self._process is None:
            _LOGGER.debug("No process is currently running.")
            return

        _LOGGER.debug("Attempting to terminate process with PID: %s", self._process.pid)

        # Graceful shutdown with SIGINT
        try:
            self._process.send_signal(signal.SIGINT)
        except ProcessLookupError:
            _LOGGER.debug("Process no longer exists.")
            self._process = None
            return

        try:
            await asyncio.wait_for(self._process.wait(), timeout=5)
            _LOGGER.debug("Process terminated gracefully.")
        except TimeoutError:
            _LOGGER.debug("Process didn't respond to SIGINT, sending SIGTERM.")

            # Not so graceful shutdown with SIGTERM
            self._process.terminate()
            try:
                await asyncio.wait_for(self._process.wait(), timeout=5)
                _LOGGER.debug("Process terminated.")
            except TimeoutError:
                _LOGGER.debug("Process didn't respond to SIGTERM, sending SIGKILL.")

                # Forceful shutdown with SIGKILL
                self._process.kill()
                await self._process.wait()
                _LOGGER.debug("Process forcefully terminated.")

        finally:
            self._process = None


async def create_hoymiles_mqtt_process_manager(
    params: Mapping[str, Any],
) -> ProcessManager:
    """
    Create ProcessManager for hoymiles-mqtt executble.

    Args:
        params: parameters and values to be passed to hoymiles-mqtt

    """
    param_list = []
    for key, value in params.items():
        param_list.append(key)
        if value != NO_CONFIG_VALUE:
            param_list.append(str(value))

    return ProcessManager([sys.executable, "-m", "hoymiles_mqtt", *param_list])
