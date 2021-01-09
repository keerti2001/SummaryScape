#!/usr/bin/env python
from __future__ import unicode_literals
import argparse
import os
import re
from itertools import starmap
import multiprocessing
import pysrt
import imageio
import youtube_dl
import chardet
import nltk
import json

imageio.plugins.ffmpeg.download()
nltk.download('punkt')

from sumy.parsers.plaintext import PlaintextParser

from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from moviepy.editor import VideoFileClip, concatenate_videoclips

imageio.plugins.ffmpeg.download()


def time(seg):
    return sum(starmap(lambda start, end: end - start, seg))


def find(filen, range=30, language="english"):
    files = pysrt.open(filen)

    enc = chardet.detect(open(filen, "rb").read())['encoding']
    files = pysrt.open(filen, encoding=enc)

    subs_range = time(
        map(to_range, files)) / len(files)
    number_of_sentences = range / subs_range
    summary = sums(files, number_of_sentences, language)
    total_range = time(summary)
    is_short = total_range < range
    if is_short:
        while total_range < range:
            number_of_sentences += 1
            summary = sums(files, number_of_sentences, language)
            total_range = time(summary)
    else:
        while total_range > range:
            number_of_sentences -= 1
            summary = sums(files, number_of_sentences, language)
            total_range = time(summary)
    return summary


def make(filen, seg):
    subt = []
    inputv = VideoFileClip(filen)
    last = 0
    for (start, end) in seg:
        subclip = inputv.subclip(start, end)
        subt.append(subclip)
        last = end
    return concatenate_videoclips(subt)


def get(filename="1.mp4", sts="1.srt"):
    seg = find(sts, 60, "english")
    summary = make(filename, seg)
    base, ext = os.path.splitext(filename)
    output = "{0}_summarized.mp4".format(base)
    summary.to_videofile(
        output,
        codec="libx264",
        temp_audiofile="temp.m4a", remove_temp=True, audio_codec="aac")
    return output


def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': url[-9:-2] + '.%(ext)s',
        'writesubtitles': True

    }

    movie = ""
    subs = ""
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info("{}".format(url), download=True)
        movie = ydl.prepare_filename(result)
        info = result.get("requested_subtitles")

        language = list(info.keys())[0]
        ext = info.get(language).get("ext")
        subs = movie.replace(".mp4", ".%s.%s" %
                             (language,
                              ext))
    return movie, subs


def sums(files, number_of_sentences, language="english"):
    p = PlaintextParser.from_string(
        to_txt(files), Tokenizer(language))
    stem = Stemmer(language)
    summarizer = LsaSummarizer(stem)
    summarizer.stop_words = get_stop_words(language)
    segment = []
    for sentence in summarizer(p.document, number_of_sentences):
        index = int(re.findall("\(([0-9]+)\)", str(sentence))[0])
        item = files[index]
        segment.append(to_range(item))
    print(segment)
    return segment


def to_txt(files):
    t = ''
    for index, item in enumerate(files):
        if item.text.startswith("["):
            continue
        t += "(%d) " % index
        t += item.text.replace("\n", "").strip("...").replace(
            ".", "").replace("?", "").replace("!", "")
        t += ". "

    return t


def to_range(item):
    starts = item.start.hours * 60 * 60 + item.start.minutes * \
             60 + item.start.seconds + item.start.milliseconds / 1000.0
    ends = item.end.hours * 60 * 60 + item.end.minutes * \
           60 + item.end.seconds + item.end.milliseconds / 1000.0
    print(starts, ends)
    return starts, ends


def final(url):
    movie, subs = download_video(url)
    if subs == "":
        return "Please provide the url of a video with subtitles"
    summary = multiprocessing.Process(target=get, args=(movie, subs))
    summary.start()
    summary.join()


# print(final('https://www.youtube.com/watch?v=5pEPpNpbnCI'))
# print(final('https://www.youtube.com/watch?v=VlZ1SWLBfPE'))
