from filebot import *


def Start():
  Log("FileBot Xattr Metadata Agent - CPU: %s, OS: %s" % (Platform.CPU, Platform.OS))


#####################################################################################################################


class XattrMovieAgent(Agent.Movies):
  name = 'FileBot Xattr Metadata (Movies)'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.imdb', 'com.plexapp.agents.themoviedb', 'com.plexapp.agents.localmedia', 'com.plexapp.agents.none']


  def search(self, results, media, lang):
    Log("[SEARCH]")

    if media.items is None:
      return

    file = media.items[0].parts[0].file
    Log("[FILE] %s" % file)

    attr = xattr_metadata(file)
    Log("[XATTR] %s" % attr)

    if attr is None:
      return

    mid = movie_id(attr)
    Log("[ID] %s" % mid)

    if mid is None:
      return

    results.Append(MetadataSearchResult(id=mid, name=movie_name(attr), year=movie_year(attr), lang=lang, score=100))


  def update(self, metadata, media, lang):
    Log("[UPDATE]")

    if media.items is None:
      return

    file = media.items[0].parts[0].file
    Log("[FILE] %s" % file)

    attr = xattr_metadata(file)
    Log("[XATTR] %s" % attr)

    if attr is None:
      return

    mid = movie_id(attr)
    Log("[ID] %s" % mid)

    if mid is None:
      return

    metadata.id = mid
    metadata.title = movie_name(attr)
    metadata.year = movie_year(attr)


#####################################################################################################################


class XattrSeriesAgent(Agent.TV_Shows):
  name = 'FileBot Xattr Metadata (TV)'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.thetvdb', 'com.plexapp.agents.themoviedb', 'com.plexapp.agents.localmedia', 'com.plexapp.agents.none']


  def search(self, results, media, lang):
    for s in media.seasons:
      for e in media.seasons[s].episodes:
        for i in media.seasons[s].episodes[e].items:
          for part in i.parts:
            Log("[SEARCH] %s | %s" % (s, e))

            file = part.file
            Log("[FILE] %s" % file)

            attr = xattr_metadata(file)
            Log("[XATTR] %s" % attr)

            if attr is None:
              continue

            sid = series_id(attr)
            Log("[ID] %s" % sid)

            if sid is None:
              continue

            results.Append(MetadataSearchResult(id=sid, name=series_name(attr), year=series_year(attr), lang=lang, score=100))


  def update(self, metadata, media, lang):
    for s in media.seasons:
      for e in media.seasons[s].episodes:
        for i in media.seasons[s].episodes[e].items:
          for part in i.parts:
            Log("[UPDATE] %s | %s" % (s, e))

            file = part.file
            Log("[FILE] %s" % file)

            attr = xattr_metadata(file)
            Log("[XATTR] %s" % attr)

            if attr is None:
              return

            sid = series_id(attr)
            Log("[ID] %s" % sid)

            if sid is None:
              continue

            metadata.id = sid
            metadata.title = series_name(attr)
            metadata.originally_available_at = series_date(attr)
            metadata.content_rating = series_certification(attr)
            metadata.studio = series_network(attr)
            metadata.duration = series_runtime(attr)
            metadata.rating = series_rating(attr)
            metadata.genres = series_genres(attr)

            episode = metadata.seasons[s].episodes[e]

            episode.title = episode_title(attr)
            episode.absolute_index = episode_absolute_number(attr)
            episode.originally_available_at = episode_date(attr)
