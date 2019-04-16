import os
import bcrypt

from pyftpdlib.authorizers import AuthenticationFailed


class MysqlAuthorizer(object):
    def __init__(self, database):
        self.database = database

    def get_user(self, username):
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM `ftp_server` WHERE `user`=%s LIMIT 1", username)
        result = cursor.fetchone()
        return result

    def validate_authentication(self, username, password, handler):
        msg = "Authentication failed."
        user = self.get_user(username)
        if user is None:
            raise AuthenticationFailed(msg)
        password = password.encode("utf-8")
        if not bcrypt.checkpw(password, user["password"].encode("utf-8")):
            raise AuthenticationFailed(msg)

    def remove_user(self, username):
        pass

    def get_home_dir(self, username):
        return self.get_user(username)["home"]

    def impersonate_user(self, username, password):
        """Impersonate another user (noop).

        It is always called before accessing the filesystem.
        By default it does nothing.  The subclass overriding this
        method is expected to provide a mechanism to change the
        current user.
        """

    def terminate_impersonation(self, username):
        """Terminate impersonation (noop).

        It is always called after having accessed the filesystem.
        By default it does nothing.  The subclass overriding this
        method is expected to provide a mechanism to switch back
        to the original user.
        """

    def has_user(self, username):
        return self.get_user(username) is not None

    def has_perm(self, username, perm, path=None):
        # if path is None:
        #     return perm in self.get_perms(username)
        # path = os.path.normcase(path)
        # home = os.path.normcase(self.get_home_dir(username))
        # if not _issubpath(path, home):
        #     return False
        return perm in self.get_perms(username)

    def get_perms(self, username):
        """Return current user permissions."""
        return "elradfmwMT"

    def get_msg_login(self, username):
        try:
            return self.get_user(username)['msg_quit']
        except KeyError:
            return "Login successful."

    def get_msg_quit(self, username):
        try:
            return self.get_user(username)['msg_quit']
        except KeyError:
            return "Goodbye."


def _issubpath(a, b):
    """Return True if a is a sub-path of b or if the paths are equal."""
    p1 = a.rstrip(os.sep).split(os.sep)
    p2 = b.rstrip(os.sep).split(os.sep)
    return p1[:len(p2)] == p2
