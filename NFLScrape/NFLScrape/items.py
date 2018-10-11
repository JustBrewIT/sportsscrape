# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NFLScrapeItem(scrapy.Item):
    #Address
    AddressLine = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    Postal = scrapy.Field()
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()
    StreetNumber = scrapy.Field()
    SteetName = scrapy.Field()
    StreetSuffix = scrapy.Field()

    # Mandatory
    SiteID = scrapy.Field()
    SiteTypeID = scrapy.Field()
    AgentID = scrapy.Field()

    # Player
    FirstName = scrapy.Field()
    LastName = scrapy.Field()
    TeamName = scrapy.Field()
    PositionName = scrapy.Field()
    Height = scrapy.Field()
    Weight = scrapy.Field()
    Age = scrapy.Field()

    # Game
    HomeTeamName = scrapy.Field()
    AwayTeamName = scrapy.Field()
    GameDate = scrapy.Field()
    GameDuration = scrapy.Field()
    SurfaceName = scrapy.Field()
    StaiumName = scrapy.Field()

    # General
    Date = scrapy.Field()

    # Offensive Stats
    Pass_Yards = scrapy.Field()
    Pass_Attempts = scrapy.Field()
    Pass_Completions = scrapy.Field()
    Pass_Touchdowns = scrapy.Field()
    Pass_Interceptions = scrapy.Field()
    Pass_FirstDowns = scrapy.Field()
    Pass_20 = scrapy.Field()
    Pass_40 = scrapy.Field()
    Pass_Rating = scrapy.Field()
    Pass_Sacks = scrapy.Field()
    Pass_Long = scrapy.Field()
    Rush_Yards = scrapy.Field()
    Rush_Attempts = scrapy.Field()
    Rush_Touchdowns = scrapy.Field()
    Rush_FirstDowns = scrapy.Field()
    Rush_Long = scrapy.Field()
    Receiving_Yards = scrapy.Field()
    Receiving_Attempts = scrapy.Field()
    Receiving_Touchdowns = scrapy.Field()
    Receiving_FirstDowns = scrapy.Field()
    Receiving_Long = scrapy.Field()
    SacksOffense = scrapy.Field()
    Fumbles = scrapy.Field()
    Pass_TwoPointConversion = scrapy.Field()
    Kick_FieldGoalYards = scrapy.Field()
    Kick_FieldGoalsAttempted = scrapy.Field()
    Kick_FieldGoalsMade = scrapy.Field()
    Kick_FieldGoalsLong = scrapy.Field()
    Kick_ExtraPointsMade = scrapy.Field()
    Kick_ExtraPointsAttempted = scrapy.Field()
    KickReturn_Yards = scrapy.Field()
    KickReturn_Attempted = scrapy.Field()
    KickReturn_Touchback = scrapy.Field()
    Kick_Touchback = scrapy.Field()
    KickReturn_Touchdowns = scrapy.Field()
    PuntReturn_Touchdowns = scrapy.Field()
    PuntReturn_Yards = scrapy.Field()
    PuntReturn_Attempts = scrapy.Field()
    PuntReturn_FairCatch = scrapy.Field()
    Punt_FairCatch = scrapy.Field()
    Punt_Long = scrapy.Field()
    Punt_Touchbacks = scrapy.Field()
    Punt_ReturnYards = scrapy.Field()
    Rush_TwoPointConversion = scrapy.Field()
    Receiving_TwoPointConversion = scrapy.Field()

    # Defensive Stats
    Tackle_Assisted = scrapy.Field()
    Tackle_Unassisted = scrapy.Field()
    Tackle_ForLoss = scrapy.Field()
    SacksDefense = scrapy.Field()
    PassDefended = scrapy.Field()
    PassIntercepted = scrapy.Field()
    PassIntercepted_Yards = scrapy.Field()
    PassIntercepted_Touchdowns = scrapy.Field()
    Fumble_Forced = scrapy.Field()
    Fumble_Recovered = scrapy.Field()
    Fumble_Touchdowns = scrapy.Field()
    Fumble_Yards = scrapy.Field()
    Block_FieldGoals = scrapy.Field()
    Block_Punts = scrapy.Field()
    Block_ExtraPoints = scrapy.Field()
    Safety = scrapy.Field()







