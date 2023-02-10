from django.shortcuts import render
from home.models import Form
from django.core.mail import EmailMessage


# Create your views here.

import moviepy.editor as mp
import os
import youtube_dl


def download_video(keyword, num_downloads):
    ydl_opts = {
        'format': '144p[ext=mp4]+bestaudio[ext=m4a]/144p[ext=mp4]/best',
        'outtmpl': 'uploads/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'audioquality': 0,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        search_url = f'ytsearch3:{keyword}'
        info = ydl.extract_info(search_url, download=False)
        videos = info['entries']
        for i, video in enumerate(videos[:num_downloads]):
            video_url = video['webpage_url']
            video_file = ydl.prepare_filename(video)
            ydl.download([video_url])
            new_video_file = f"{keyword} {i+1}.mp4"
            os.rename(video_file, new_video_file)
            print(
                f'Video {i+1} downloaded successfully and renamed to "{new_video_file}"')


def convert_to_audio(video_file):
    clip = mp.VideoFileClip(video_file)
    audio_file = video_file.split('.mp4')[0] + '.wav'
    clip.audio.write_audiofile(audio_file)
    # clip.reader.close()
    return audio_file


def cut_audio(audio_file, cut_time):
    clip = mp.AudioFileClip(audio_file)
    clip = clip.subclip(0, cut_time)
    #clip.reader.close()
    return clip


def merge_clips(clips, output_file):
    final_clip = mp.concatenate_audioclips(clips)
    final_clip.write_audiofile(f'uploads/{output_file}')
    

def delete_extra_files(keyword, size):
    for i in range(1, size + 1):
        video_file = f'{keyword} {i}.mp4'
        #audio_file = video_file.split('.mp4')[0] + '.wav'
        if os.path.exists(video_file):
            os.remove(video_file)
        #if os.path.exists(audio_file):
        #    os.remove(audio_file)

# def delete_audio_files(keyword, size):
#     for i in range(1, size + 1):
#         audio_file = f'{keyword} {i}.wav'
#         if os.path.exists(audio_file):
#             os.remove(audio_file)


def index(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        size = int(request.POST.get('size'))
        duration = int(request.POST.get('duration'))
        email = request.POST.get('email')
        index = Form(keyword=keyword, size=size,
                     duration=duration, email=email)
        index.save()

        download_video(keyword, size)

        clips = []
        for i in range(1, size + 1):
            video_file = f'{keyword} {i}.mp4'
            audio_file = convert_to_audio(video_file)
            clip = cut_audio(audio_file, duration)
            clips.append(clip)
            
            

        merge_clips(clips, 'result.wav')
        

        send_email = EmailMessage(
            'Thank you for using this service',
            'Here is your audio',
            to=[email]
        )
        send_email.attach_file(f'uploads/result.wav')
        send_email.send()
        
        os.remove('uploads/result.wav')
        delete_extra_files(keyword, size)
        
    return render(request, 'index.html')


