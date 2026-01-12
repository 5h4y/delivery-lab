import re
import idna
from email_validator import validate_email, EmailNotValidError


''' I started to work on a dedicated script for syntax validation before realizing that there's already a great library for that. Keeping this around to use side-by-side for learning + exploring.

'''

EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@"
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,}$)"
)

def validate_email_syntax(email):
    try:
        local_part, domain = email.rsplit("@", 1)
    except ValueError:
        return False, "Missing '@' symbol."

    if ".." in local_part or local_part.startswith(".") or local_part.endswith("."):
        return False, "Invalid local part: consecutive or leading/trailing dots."

    try:
        ascii_domain = idna.encode(domain).decode("ascii")
    except idna.IDNAError:
        return False, "Invalid domain name (IDN conversion failed)."

    if not EMAIL_REGEX.match(f"{local_part}@{ascii_domain}"):
        return False, "Does not match expected email syntax."

    return True, "Valid syntax."


def library_validate_email(email, check_dns=False):
    try:
        result = validate_email(email, check_deliverability=check_dns)
        return True, f"Valid email: {result['email']}"
    except EmailNotValidError as e:
        return False, str(e)

# interface for switching between my initial attempt and the email_validator library.
def validate_email_syntax(email, use_library=True, check_dns=False):
    if use_library:
        return library_validate_email(email, check_dns)
    else:
        return validate_email_syntax(email)


# cli entry point
if __name__ == "__main__":
    email = input("Enter an email address to check syntax: ").strip()
    
    # FLAG for switching methods
    USE_LIBRARY = False  
    CHECK_DNS = True # basic script doesn't have this functionality, ignore if not using library  

    valid, message = validate_email_syntax(email, use_library=USE_LIBRARY, check_dns=CHECK_DNS)
    if valid:
        print(f"OK {message}")
    else:
        print(f"ERROR {message}")
