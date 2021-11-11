import click
import sys
import msal

@click.command()
def main():
    """Example of MSAL for Python usage."""

    print('Hello, world.')
    return 0

if __name__ == "__main__":
    sys.exit(main())