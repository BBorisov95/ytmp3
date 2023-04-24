from pytube import YouTube
import os


def dwn(link, folder_name):
    yt = YouTube(link)

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    # check for destination to save file
    destination = folder_name or '.'

    # download the file
    out_file = video.download(output_path=destination)

    # save the
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    try:
        os.rename(out_file, new_file)
    except FileExistsError:
        out_file = video.download(output_path=f"{folder_name}\dublications")
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

    print(yt.title + " has been successfully downloaded.")


links_file = open("links.txt", "r")
links = links_file.readlines()
folder_name = input("Set Folder Name: ")
failed = []
for link in links:
    try:
        dwn(link, folder_name)
    except KeyError:
        failed.append(link)

if len(failed) == 0:
    print("All done, without errors")
else:
    print(f"Got {len(failed)} failed extractions and will try again.")
    while len(failed) > 0:
        for link in failed:
            print(f"Trying again: {link}")
            try:
                dwn(link, folder_name)
                failed.remove(link)
            except KeyError:
                continue
        print(f"Tried again to extract the failed ones. Got {len(failed)} left")
