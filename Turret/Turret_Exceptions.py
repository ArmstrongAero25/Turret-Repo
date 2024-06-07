# Calm1403: These are just some exceptions that I quickly wrote.

class servoException(Exception):
    """
    Should be called in the
    event that the servo doesn't
    do, what the fuck it's supposed to.
    """

    def __str__(self):
        return "\033[1;91mError\003[0m turning servo."


class videoException(Exception):
    """
    Should be called in the event
    that the video isn't captured.
    """

    def __str__(self):
        return "\033[1;91mError\033[0m opening capture."
