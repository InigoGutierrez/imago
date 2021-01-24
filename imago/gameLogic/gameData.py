"""Invariable data pertaining a match."""

class GameData:
    """Invariable data pertaining a match."""

    def __init__(self,
            name = None,
            size = 19,
            annotator = None,
            date = None,
            blackRank = "?",
            whiteRank = "?",
            blackName = None,
            whiteName = None,
            blackTeam = None,
            whiteTeam = None,
            copyrightInfo = None,
            event = None,
            gameComment = None,
            openingInfo = None,
            timeInfo = None,
            overtimeInfo = None,
            placeInfo = None,
            result = "?",
            roundInfo = None,
            rules = None,
            source = None,
            user = None
        ):
        self.name = name
        self.size = size
        self.annotator = annotator
        self.date = date
        self.blackRank = blackRank
        self.whiteRank = whiteRank
        self.blackName = blackName
        self.whiteName = whiteName
        self.blackTeam = blackTeam
        self.whiteTeam = whiteTeam
        self.copyrightInfo = copyrightInfo
        self.event = event
        self.gameComment = gameComment
        self.openingInfo = openingInfo
        self.timeInfo = timeInfo
        self.overtimeInfo = overtimeInfo
        self.placeInfo = placeInfo
        self.result = result
        self.roundInfo = roundInfo
        self.rules = rules
        self.source = source
        self.user = user
