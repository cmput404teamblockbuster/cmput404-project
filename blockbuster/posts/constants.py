(PRIVATE_TO_ALL_FRIENDS, PRIVATE_TO, PRIVACY_PUBLIC, PRIVATE_TO_FOF, PRIVATE_TO_ME, PRIVACY_UNLISTED, PRIVACY_SERVER_ONLY) = (
    'FRIENDS', 'PRIVATE', 'PUBLIC', 'FOF', 'PRIVATE',
    'privacy_unlisted', 'SERVERONLY')

PRIVACY_TYPES = {
    PRIVATE_TO_ALL_FRIENDS: {
        'name': 'Friends',
    },
    PRIVATE_TO: {
        'name': 'Specified Users'
    },
    PRIVACY_PUBLIC: {
        'name': 'Public'
    },
    PRIVATE_TO_FOF: {
        'name': 'Friends-of-Friends'
    },
    PRIVATE_TO_ME: {
        'name': 'Me'
    },
    PRIVACY_UNLISTED: {
        'name': 'Unlisted'
    },
    PRIVACY_SERVER_ONLY: {
        'name': 'Server Only'
    },
}

text_markdown = "text/markdown"
text_plain = "text/plain"
binary = "application/base64"
png = "image/png;base64"
jpeg = "image/jpeg;base64"

contentchoices = (
    (text_markdown, 'text/markdown'),
    (text_plain, 'text/plain'),
    (binary, 'application/base64'),
    (png, 'image/png;base64'),
    (jpeg, 'image/jpeg;base64'),
)
