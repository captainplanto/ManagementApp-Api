# test custom Django management commands
# from psycopg2 import OperationalError as Psycopg2Error
# from django.db.utils import OperationalError
from unittest.mock import patch
from django.core.management import call_command
from django.test import SimpleTestCase

# Test if database is ready to connect


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])


"""

# Test if database database is not ready to connect
@patch("time.sleep")
    def test_wait_db_delay(self, patched_sleep, patched_check):
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
        """
