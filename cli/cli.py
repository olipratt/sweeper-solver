"""
A CLI for input/output of messages.
"""

import queue
import threading
import sys
import logging


log = logging.getLogger(__name__)


# How long to block waiting for a message on a queue before checking that we're
# still running - in seconds.
OUTPUT_QUEUE_BLOCK_TIME = 0.25


class CLIInput(object):
    """ An object that provides a command line interface to read in commands
        from users and write responses back out. """

    def __init__(self, to_user_q, from_user_q,
                 stdin=sys.stdin, stdout=sys.stdout):
        """ Initialise a new CLI Input. """
        log.debug('Initialising a new CLI instance')

        # Store the stdin and stdout to read from/write to.
        self.stdin = stdin
        self.stdout = stdout

        # Queues to read messages from to output to the user, or put messages
        # from the user on to.
        self.to_user_queue = to_user_q
        self.from_user_queue = from_user_q

        # Flag indicating if the CLI is running.
        self.running = False

        # Threads that handle the input and output.
        self.to_user_thread = None
        self.from_user_thread = None

    def start(self):
        """ Starts the CLI.

        It will run until it gets an EOF at the prompt, or is stopped by a call
        to stop.
        """
        log.debug("Starting CLI")
        if not self.running:
            log.debug("CLI is not running")
            self.running = True
            self._start_threads()

        log.debug('CLI is started')

    def _start_threads(self):
        """ Start the threads that get from/put on the input/output queues. """
        log.debug("Starting CLI threads")
        self.to_user_thread = \
            threading.Thread(target=self._output_commands_to_prompt)
        self.to_user_thread.daemon = True

        self.from_user_thread = \
            threading.Thread(target=self._read_commands_from_prompt)
        self.from_user_thread.daemon = True

        self.to_user_thread.start()
        self.from_user_thread.start()

    def stop(self):
        """ Stops the CLI. """
        log.debug("Stopping CLI")
        if self.running:
            log.debug("CLI is running - stopping")
            self.running = False
            self._join_threads()

        log.debug("CLI is stopped")

    def _join_threads(self):
        """ Wait briefly for threads to exit. Ignore failures. """
        try:
            self.to_user_thread.join(2 * OUTPUT_QUEUE_BLOCK_TIME)
        except RuntimeError:
            log.exception("To user thread didn't exit - ignoring")
        try:
            self.from_user_thread.join(2 * OUTPUT_QUEUE_BLOCK_TIME)
        except RuntimeError:
            log.exception("From user thread didn't exit - ignoring")

    def is_running(self):
        """ Returns whether the CLI has been started. """
        log.debug('Returning if CLI is running: %s', self.running)
        return self.running

    def _read_commands_from_prompt(self):
        """ Loops continuously, getting input from stdin and storing the
            strings provided in an internal queue.
            Stops running if we get an EOF, and puts None onto the queue.
        """
        log.debug('Starting command input loop')
        while self.running:
            # This read will block indefinitely and there's no nice way to
            # periodically drop out that I've found. This might cause problems
            # if the CLI is started, stopped, and restarted...
            raw_command = self.stdin.readline()

            if raw_command == '':
                log.debug("Got EOF - exiting")
                self.from_user_queue.put(None)
                break

            command = raw_command.rstrip('\n')
            log.debug('Got command from prompt: %s', command)
            self.from_user_queue.put(command)

        log.debug("Stopping input reading loop")

    def _output_commands_to_prompt(self):
        """ Loops continuously, writing out responses from the internal output
            queue to the prompt.
        """
        log.debug('Starting command output loop')
        while self.running:
            try:
                # Block waiting for a message to output, but regularly drop
                # out to make sure we're still running.
                response = self.to_user_queue.get(OUTPUT_QUEUE_BLOCK_TIME)
            except queue.Empty:
                pass
            else:
                log.debug('Writing out response: %s', response)
                self.stdout.write('{}\n'.format(response))
                self.stdout.flush()

        log.debug("Stopping output writing loop")
