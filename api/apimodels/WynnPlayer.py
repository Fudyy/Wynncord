from typing import Optional, List, Dict
from datetime import datetime
from dateutil import tz


class LegacyRankColour:
    def __init__(self, **kwargs):
        self.main_color: str = kwargs.get('main')
        self.sub_color: str = kwargs.get('sub')


class GlobalData:
    def __init__(self, **kwargs):
        self.wars: int = kwargs.get('wars')
        self.total_level: int = kwargs.get('totalLevel')
        self.mobs_killed: int = kwargs.get('mobsKilled')
        self.chests_found: int = kwargs.get('chestsFound')
        self.dungeons: Dict = kwargs.get('dungeons')
        self.raids: Dict = kwargs.get('raids')
        self.completed_quests: int = kwargs.get('completedQuests')
        self.pvp: PvP = PvP(**kwargs.get('pvp'))


class Ranking:
    def __init__(self, **kwargs):
        self.woodcutting_level: int = kwargs.get('woodcuttingLevel')
        self.scribing_level: int = kwargs.get('scribingLevel')
        self.fishing_level: int = kwargs.get('fishingLevel')
        self.mining_level: int = kwargs.get('miningLevel')
        self.farming_level: int = kwargs.get('farmingLevel')
        self.wars_completion: int = kwargs.get('warsCompletion')
        self.tcc_completion: int = kwargs.get('tccCompletion')
        self.combat_solo_level: int = kwargs.get('combatSoloLevel')
        self.nol_completion: int = kwargs.get('nolCompletion')
        self.nog_completion: int = kwargs.get('nogCompletion')
        self.tna_completion: int = kwargs.get('tnaCompletion')
        self.total_solo_level: int = kwargs.get('totalSoloLevel')
        self.professions_solo_level: int = kwargs.get('professionsSoloLevel')
        self.total_global_level: int = kwargs.get('totalGlobalLevel')
        self.professions_global_level: int = kwargs.get('professionsGlobalLevel')
        self.player_content: int = kwargs.get('playerContent')
        self.combat_global_level: int = kwargs.get('combatGlobalLevel')
        self.woodworking_level: int = kwargs.get('woodworkingLevel')
        self.tailoring_level: int = kwargs.get('tailoringLevel')
        self.alchemism_level: int = kwargs.get('alchemismLevel')
        self.armouring_level: int = kwargs.get('armouringLevel')
        self.jeweling_level: int = kwargs.get('jewelingLevel')


class Professions:
    def __init__(self, **kwargs):
        self.alchemism: Profession = Profession(**kwargs.get("alchemism"))
        self.armouring: Profession = Profession(**kwargs.get("armouring"))
        self.cooking: Profession = Profession(**kwargs.get("cooking"))
        self.jeweling: Profession = Profession(**kwargs.get("jeweling"))
        self.scribing: Profession = Profession(**kwargs.get("scribing"))
        self.tailoring: Profession = Profession(**kwargs.get("tailoring"))
        self.weaponsmithing: Profession = Profession(**kwargs.get("weaponsmithing"))
        self.woodworking: Profession = Profession(**kwargs.get("woodworking"))


class PlayerGuild:
    def __init__(self, **kwargs):
        self.uuid: str = kwargs.get('uuid')
        self.name: str = kwargs.get('name')
        self.prefix: str = kwargs.get('prefix')
        self.rank: str = kwargs.get('rank')
        self.rank_stars: str = kwargs.get('rankStars')


class Profession:
    def __init__(self, **kwargs):
        self.level: int = kwargs.get("level")
        self.xp_percent: int = kwargs.get("xpPercent")


class SkillPoints:
    def __init__(self, **kwargs):
        self.strength: int = kwargs.get("strength")
        self.dexterity: int = kwargs.get("dexterity")
        self.intelligence: int = kwargs.get("intelligence")
        self.agility: int = kwargs.get("agility")


class PvP:
    def __init__(self, **kwargs):
        self.kills: int = kwargs.get("kills")
        self.deaths: int = kwargs.get("deaths")


class Character:
    def __init__(self, **kwargs):
        self.type: str = kwargs.get('type')
        self.nickname: Optional[str] = kwargs.get('nickname')
        self.level: int = kwargs.get('level')
        self.xp: int = kwargs.get('xp')
        self.xp_percent: int = kwargs.get('xpPercent')
        self.total_level: int = kwargs.get('totalLevel')
        self.wars: int = kwargs.get('wars')
        self.playtime: float = kwargs.get('playtime')
        self.mobs_killed: int = kwargs.get('mobsKilled')
        self.chests_found: int = kwargs.get('chestsFound')
        self.items_identified: int = kwargs.get('itemsIdentified')
        self.blocks_walked: int = kwargs.get('blocksWalked')
        self.logins: int = kwargs.get('logins')
        self.deaths: int = kwargs.get('deaths')
        self.discoveries: int = kwargs.get('discoveries')
        self.pre_economy: bool = kwargs.get('preEconomy')
        self.pvp: PvP = PvP(**kwargs.get('pvp'))
        self.gamemode: List[str] = kwargs.get('gamemode')
        self.skill_points: SkillPoints = kwargs.get('skillPoints')
        self.professions: Professions = Professions(**kwargs.get('professions'))
        self.dungeons: Dict = kwargs.get('dungeons')
        self.raids: Dict = kwargs.get('raids')
        self.quests: List[str] = kwargs.get('quests')


class WynnPlayer:
    def __init__(self, **kwargs):
        self.username: str = kwargs.get('username', '')
        self.online: bool = kwargs.get('online')
        self.server: Optional[str] = kwargs.get('server')
        self.active_character: Optional[str] = kwargs.get('activeCharacter')
        self.uuid: str = kwargs.get('uuid')
        self.rank: str = kwargs.get('rank')
        self.rank_badge: Optional[str] = kwargs.get('rankBadge')
        self.legacy_rank_colour: Optional[LegacyRankColour] = LegacyRankColour(
            **kwargs.get("legacyRankColour")) if kwargs.get("legacyRankColour") else None
        self.shortened_rank: Optional[str] = kwargs.get('shortenedRank')
        self.support_rank: Optional[str] = kwargs.get('supportRank')
        self.veteran: bool = kwargs.get('veteran')
        self.first_join: datetime = to_local_time(kwargs.get('firstJoin'))
        self.last_join: datetime = to_local_time(kwargs.get('lastJoin'))
        self.playtime: float = kwargs.get('playtime')
        self.guild: Optional[PlayerGuild] = PlayerGuild(**kwargs.get('guild')) if kwargs.get('guild') else None
        self.global_data: GlobalData = GlobalData(**kwargs.get('globalData'))
        self.forum_link: Optional[int] = kwargs.get('forumLink')
        self.ranking: Ranking = Ranking(**kwargs.get('ranking'))
        self.public_profile: bool = kwargs.get('publicProfile')
        self.characters: List[Character] = [Character(**kwargs.get('characters')[key]) for key in
                                            kwargs.get('characters')]


def to_local_time(datestring: str) -> datetime:
    """
    Converts the date string to a datetime with local timezone.
    """
    raw_date = datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S.%fZ')
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = raw_date.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)
