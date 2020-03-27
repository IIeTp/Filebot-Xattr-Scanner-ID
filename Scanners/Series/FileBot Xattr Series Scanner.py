import re, Media, VideoFiles

from filebot import *


def Scan(path, files, mediaList, subdirs, language=None, root=None):
  VideoFiles.Scan(path, files, mediaList, subdirs, root)

  for file in files:
    attr = xattr_metadata(file)
    if attr is None:
      continue

    print("[XATTR] %s" % attr)

    # single episode | multi episode
    episodes = list_episodes(attr)
    multi_episode_count = len(episodes)

    for i, attr in enumerate(episodes):
      guid = series_guid(attr)
      name = series_name(attr)
      special = episode_special_number(attr)
      year = series_year(attr)

      # use series id as series name value (only supported by TheTVDB agent)
      m = re.search('com.plexapp.agents.thetvdb://([0-9]+)', guid)
      x = re.search('com.plexapp.agents.themoviedb://([0-9]+', guid)
      y = re.search('com.plexapp.agents.hama://([0-9]+)', guid)
      
      if m:
        name = u"%s [tvdb-%05d]" % (name, int(m.group(1)))                 # TheTVDB IDs start at 70327
        year = None
      elif x:
        name = u"%s [tmdb-%05d]" % (name, int(m.group(1)))
        year = None
      elif y:
        name = u"%s [anidb-%05d]" % (name, int(m.group(1))) 
        year = None
       
      media = Media.Episode(
        name.encode('utf-8'),                           # use str since Plex doesn't like unicode strings
        0 if special else episode_season_number(attr),
        special if special else episode_number(attr),
        episode_title(attr).encode('utf-8'),            # use str since Plex doesn't like unicode strings
        series_year(attr)
      )

      date = episode_date(attr)
      if date:
        media.released_at = date.strftime('%Y-%m-%d')

      if (multi_episode_count > 1):
        media.display_offset = (i * 100) / multi_episode_count

      original_filename = xattr_filename(file)
      if original_filename:
        media.source = VideoFiles.RetrieveSource(original_filename.encode('utf-8'))

      media.parts.append(file)
      mediaList.append(media)

      print("[MEDIA] %s | %s | %s | %s" % (media, media.year, media.released_at, media.source))
