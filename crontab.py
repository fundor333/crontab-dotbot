import os
import subprocess

import dotbot


class Crontab(dotbot.Plugin):

    # Dotbot methods
    _comment = "#dotbot-crontab"
    _directive = "crontab"
    _temp_file = 'out.txt'

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            self._log.error("We can't handle {}".format(directive))
            return False
        try:
            cronjob_rows = []
            for entry in data:
                row = "{} {} {}".format(
                    entry["cron"], entry["command"], self._comment)
                self._log.lowinfo("Add {}".format(row))
                cronjob_rows.append(row)
            self._read_cron_file(cronjob_rows)
            self._log.info("All cron have been sync")
            return True
        except ValueError as e:
            self._log.error(e)
            return False

    def _read_cron_file(self, rows):
        try:
            with open(self._temp_file, 'w+') as fout:
                out = subprocess.call(["crontab", '-l'], stdout=fout)
        except Exception as e:
            self._log.error(e)
        self._delete_line(self._temp_file)
        with open(self._temp_file, "w+") as file_object:
            for row in rows:
                file_object.write("\n{}".format(row))
        subprocess.call(["crontab", "-r"])
        subprocess.call(["crontab", self._temp_file])
        os.remove(self._temp_file)

    def _delete_line(self, original_file):
        try:
            is_skipped = False
            dummy_file = original_file + '.bak'
            # Open original file in read only mode and dummy file in write mode
            with open(original_file, 'r+') as read_obj, open(dummy_file, 'w+') as write_obj:
                # Line by line copy data from original file to dummy file
                for line in read_obj:
                    # If current line number matches the given line number then skip copying
                    if self._comment in line:
                        write_obj.write(line)
                    else:
                        is_skipped = True
            # If any line is skipped then rename dummy file as original file
            if is_skipped:
                os.remove(original_file)
                os.rename(dummy_file, original_file)
            else:
                os.remove(dummy_file)
        except Exception as e:
            self._log.error(e)
