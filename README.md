# FileBot Xattr Metadata Scanners

Enhance Plex with support for [FileBot Xattr Metadata](https://www.filebot.net/forums/viewtopic.php?f=3&t=324).


## Install

1. Download the [release](https://github.com/IIeTp/Filebot-Xattr-Scanner-ID/releases)
2. Copy the `Scanners` folder into the [`Plex Media Server`](https://support.plex.tv/articles/202915258-where-is-the-plex-media-server-data-directory-located/) data directory
3. Restart Plex
4. Configure `Advanced ➔ Scanner` for each library and select `FileBot Xattr Scanner ID`
```sh
#!/bin/sh -xu
curl -L -O https://github.com/IIeTp/Filebot-Xattr-Scanner-ID/archive/master.zip
unzip -o master.zip
cp -vru 'Filebot-Xattr-Scanner-ID-master/Scanners' '/path/to/PlexMediaServer/Library/Plex Media Server'
```

## FileBot Xattr Metadata Scanner ID

The `FileBot Xattr Scanner ID` will read `name / year / season / episode / etc` from xattr metadata instead of guessing and parsing information from the file path. This scanner will greatly enhance primary agents such as `Plex Movie`, `TheMovieDB` or `TheTVDB`, regardless of whether files are named according to [`{plex}`](https://www.filebot.net/forums/viewtopic.php?f=5&t=4116) standards or not. Files without xattr metadata will be ignored.
