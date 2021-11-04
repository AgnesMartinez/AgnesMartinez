from datetime import datetime
import requests


HEADERS = {
    "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAPYXBAAAAAAACLXUNDekMxqa8h%2F40K4moUkGsoc%3DTYfbDKbT3jJPCEVnMYqilB28NHfOPqkca3qaAxGfsyKCs0wRbw"
}

BASE_URL = "https://api.twitter.com/1.1/"


def main():

    request_token()

    url = BASE_URL + "statuses/user_timeline.json?screen_name=fernandeznorona&count=5&tweet_mode=extended"

    response = requests.get(url, headers=HEADERS)
    data = response.json()

    tweets = list()
    tweets.append("# Changoleón Legislativo")

    for tweet in data:

        date = datetime.strptime(
            tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y")

        tweet_id = tweet["id"]
        fullname = tweet["user"]["name"]
        username = tweet["user"]["screen_name"]
        permalink = f"https://twitter.com/{username}/status/{tweet_id}"

        favorites = tweet["favorite_count"]
        retweets = tweet["retweet_count"]

        tweet_text = tweet["full_text"].split(
            "https://t.co")[0].split("http://t.co")[0].strip()

        text_lines = list()

        for line in tweet_text.split("\n"):

            if len(line) > 0:

                if line[0] == "#":
                    text_lines.append("\#" + line[1:])
                else:
                    text_lines.append(line)
            else:
                text_lines.append("\n")

        tweet_text = "\n".join(text_lines)

        message = f"**{fullname}** (**@{username}**) • {date:%d-%m-%Y a las %H:%M:%S}\n*****\n"
        message += tweet_text
        message += f"\n*****\n[Permalink]({permalink}) | {favorites:,} Me Gusta | {retweets:,} Retweets"

        tweets.append(message)

    open("README.md", "w", encoding="utf-8").write("\n*****\n".join(tweets))


def request_token():

    with requests.post(BASE_URL + "guest/activate.json", headers=HEADERS) as response:
        guest_token = response.json()["guest_token"]
        HEADERS["x-guest-token"] = guest_token


if __name__ == "__main__":

    main()
