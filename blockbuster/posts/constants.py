(PRIVATE_TO_ALL_FRIENDS, PRIVACY_PUBLIC, PRIVATE_TO_FOF, PRIVACY_PRIVATE, PRIVACY_UNLISTED, PRIVACY_SERVER_ONLY) = (
    'FRIENDS', 'PUBLIC', 'FOAF', 'PRIVATE',
    'privacy_unlisted', 'SERVERONLY')

PRIVACY_TYPES = {
    PRIVATE_TO_ALL_FRIENDS: {
        'name': 'Friends',
    },
    PRIVACY_PUBLIC: {
        'name': 'Public'
    },
    PRIVATE_TO_FOF: {
        'name': 'Friends-of-Friends'
    },
    PRIVACY_PRIVATE: {
        'name': 'Private'
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
