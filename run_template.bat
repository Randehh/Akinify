@echo off
echo To use this Akinify, you will need the URI of the artist. You can get this by right-clicking on an artist in Spotify, going to the "Share" sub-menu, then selecting "Copy Spotify URI".
echo Paste the URI of your chosen artist below.
set /p artist_id="Enter artist URI: "

echo.
echo Choose how deep you wish the algorithm to search, I recommend 1 or 2, the former for very niche artists and the latter for less niche artists. For big artists, you can do 3 or 4.
set /p search_depth="Enter search depth: "

echo.
echo Lastly, please enter your username if this is your first time using the tool, otherwise hit enter right away.
set /p username="Enter user name: "

echo.
akinify.exe %artist_id% %search_depth% %username%
PAUSE