from __future__ import unicode_literals
import youtube_dl as yt
from HandleError import HandleErrors

def esc(code):
    return f'\033[{code}m'

print(esc('1;38;2;117;206;73') + "Music automatically goes into the music folder whereas you can choose your location for others.")

destination = input(esc('1;38;2;73;206;176') + "Destination:" + esc(0) + ' ')


## Music Videos
music_ops = {'format': 'bestvideo+bestaudio',
             'outtmpl': 'R:/Downloaded Videos/Music/%(title)s',
             'cachedir': False
}

## Videos
video_ops = {'format': 'bestvideo+bestaudio',
             'outtmpl': '{}%(title)s'.format(destination)
}


URLS = [
]


get_error = HandleErrors(destination, esc)
get_error.valid_drive()
get_error.valid_end()


download = input(esc('1;38;2;73;206;176') + "Video[1] --- Music[2]   ")

print(esc('1;38;2;117;206;73') +
      "If you wish to download a playlist, please choose SINGLE as it will "
      "automatically download all of them.... or choose MULTIPLE with 1 amount."
      )

if download == "1":
    isMultiple = input(esc('1;38;2;73;206;176') + "Single[1] ---- Multiple[2]   ")

    if isMultiple == "1":
        print(esc('1;38;2;117;206;73') +
              "This can be a playlist even, by typing the playlist name and "
              "then it will download everything in that playlist."
              )

        try:
            url = input(str(esc('1;38;2;73;206;176') + "URL: ") + esc('1;38;2;168;192;35'))

        finally:
            try:
                with yt.YoutubeDL(video_ops) as ydl:
                    ydl.download([url])
                    print(esc('1;38;2;73;206;176') + "\n\n------------------------------------\n\n")
            except:
                print(esc('1;38;2;255;107;104') + "ERROR: unable to download video data: The read operation timed out")

                         ####################################################################

    if isMultiple == "2":
        AMOUNT = input(esc('1;38;2;117;206;73') + "Number of videos to download: ")
        URL_AMOUNT = 1
        MAX_AMOUNT = 20
        if AMOUNT == "":
            print(esc('1;38;2;255;107;104') + "Umm... what?")
            quit()  # Stop your programing with quit()
            # Can also do exit()

        elif AMOUNT != "0" and AMOUNT != "1" \
                and AMOUNT != "2" and AMOUNT != "3" \
                and AMOUNT != "4" and AMOUNT != "5" \
                and AMOUNT != "6" and AMOUNT != "7" \
                and AMOUNT != "8" and AMOUNT != "9" \
                and AMOUNT != "10" and AMOUNT != "11" \
                and AMOUNT != "12" and AMOUNT != "13" \
                and AMOUNT != "14" and AMOUNT != "15" \
                and AMOUNT != "16" and AMOUNT != "17" \
                and AMOUNT != "18" and AMOUNT != "19" \
                and AMOUNT != "20":                   # The "\" is called a Continuation character.
            print(esc('1;38;2;255;107;104') + "Sorry, you can only download up to 20.")
            AMOUNT = 20

        try:
            for i in range(int(AMOUNT)):
                url = input(str(esc('1;38;2;73;206;176') + f"URL {URL_AMOUNT}: " + esc('1;38;2;168;192;35')))
                URL_AMOUNT += 1
                URLS.append(url)

        finally:

            with yt.YoutubeDL(video_ops) as ydl:
                URL_AMOUNT = 0

                for i in range(len(URLS)):
                    try:
                        ydl.download([URLS[URL_AMOUNT]])

                    except:
                        print(esc('1;38;2;255;107;104') + "ERROR: unable to download video data: The read operation timed out")

                    finally:
                        URL_AMOUNT += 1
                        print(esc('1;38;2;73;206;176') + "\n\n------------------------------------\n\n")
                quit()


###############################################################################################################################

elif download == "2":
    isMultiple = input(esc('1;38;2;73;206;176') + "Single[1] ---- Multiple[2]   ")

    if isMultiple == "1":
        print(esc('1;38;2;117;206;73') +
              "This can be a playlist even, by typing the playlist name and "
              "then it will download everything in that playlist."
                )

        try:
            url = input(str(esc('1;38;2;73;206;176') + "URL: ") + esc('1;38;2;168;192;35'))

        except:
            print(esc('1;38;2;255;107;104') + "ERROR: unable to download video data: The read operation timed out")

        finally:
            try:
                with yt.YoutubeDL(music_ops) as ydl:
                    ydl.download([url])
                    print(esc('1;38;2;73;206;176') + "\n\n------------------------------------\n\n")
            except:
                print(esc('1;38;2;255;107;104') + "ERROR: unable to download video data: The read operation timed out")

                            ####################################################################

    if isMultiple == "2":
        AMOUNT = input(esc('1;38;2;117;206;73') + "Number of videos to download: ")
        URL_AMOUNT = 1
        MAX_AMOUNT = 20
        if AMOUNT == "":
            print(esc('1;38;2;255;107;104') + "Umm... what?")
            quit()     # Stop your programming with quit()

        elif AMOUNT != "0" \
                and AMOUNT != "1" \
                and AMOUNT != "2" and AMOUNT != "3" \
                and AMOUNT != "4" and AMOUNT != "5" \
                and AMOUNT != "6" and AMOUNT != "7" \
                and AMOUNT != "8" and AMOUNT != "9" \
                and AMOUNT != "10" and AMOUNT != "11" \
                and AMOUNT != "12" and AMOUNT != "13" \
                and AMOUNT != "14" and AMOUNT != "15" \
                and AMOUNT != "16" and AMOUNT != "17" \
                and AMOUNT != "18" and AMOUNT != "19" \
                and AMOUNT != "20":
            print(esc('1;38;2;255;107;104') + "Sorry, you can only download up to 20.")
            AMOUNT = 20

        try:
            for i in range(int(AMOUNT)):
                url = input(str(esc('1;38;2;73;206;176') + f"URL {URL_AMOUNT}: ") + esc('1;38;2;168;192;35'))
                URL_AMOUNT += 1
                URLS.append(url)

        finally:

            with yt.YoutubeDL(music_ops) as ydl:
                URL_AMOUNT = 0

                for i in range(len(URLS)):
                    try:
                        ydl.download([URLS[URL_AMOUNT]])

                    except:
                        print(esc('1;38;2;255;107;104') + "ERROR: unable to download video data: The read operation timed out")

                    finally:
                        URL_AMOUNT += 1
                        print(esc('1;38;2;73;206;176') + "\n\n------------------------------------\n\n")
                quit()




else:
    print(esc('1;38;2;255;107;104') + "Invalid response.")

exit()
## Extracting data from a Video without downloading it
url2 = ydl.extract_info(url, download=False)
print('upload date : %s' % (url2['upload_date']))
print('uploader    : %s' %(url2['uploader']))
print('views       : %d' %(url2['view_count']))
print('likes       : %d' %(url2['like_count']))
print('dislikes    : %d' %(url2['dislike_count']))
print('id          : %s' %(url2['id']))
print('format      : %s' %(url2['format']))
print('duration    : %s' %(url2['duration']))
print('title       : %s' %(url2['title']))
print('description : %s' %(url2['description']))