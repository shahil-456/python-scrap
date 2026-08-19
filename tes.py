import re

def clean_locationPdf(location):
    return re.sub(r"\s*-\s*slides?.*$", "", location, flags=re.IGNORECASE).strip()


names = [
    "test-bike - slides",
    "Cardiology - Slides",
    "Heart Failure - slide Deck",
    "My Course-slid ejdhd -dlsid -slid"
]

for name in names:
    print(clean_locationPdf(name))




