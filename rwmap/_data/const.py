import rwmap._frame as frame
from typing import Union

class KEY:
    empty_tile = "0"
    empty_tile_for_tilegroup = "e"
    tag_for_tile_notre = "|"

class NAME:
    Ground = "Ground"
    PathingOverride = "PathingOverride"
    Units = "Units"
    ItemsExtra = "ItemsExtra"
    Items = "Items"
    GroundDetails = "GroundDetails"
    Triggers = "Triggers"
    unitAdd = "unitAdd"



class MAPTYPE:
    skirmish = "skirmish"
    challenge = "challenge"
    survival = "survival"
    mission = "mission"

class FOG:
    NONE = "NONE"
    map = "map"
    los = "los"

class WIN:
    NONE = "NONE"
    mainBuildings = "mainBuildings"
    allUnitsAndBuildings = "allUnitsAndBuildings"
    allBuildings = "allBuildings"
    commandCenter = "commandCenter"
    requiredObjectives = "requiredObjectives"

class COO:
    SIZE_STANDARD = frame.Coordinate(20, 20)

class TYPE:
    tileid = Union[int, tuple[str, int], frame.TagCoordinate]

class UNIT:
    turret_flamethrower = "turret_flamethrower"
    turret_artillery = "turret_artillery"
    turretT2 = "turretT2"
    turret = "turret"
    supplyDepot = "supplyDepot"
    repairbay = "repairbay"
    outpostT1 = "outpostT1"
    outpostT2 = "outpostT2"
    antiAirTurret = "antiAirTurrets"
    builder = "builder"
    landFactory = "landFactory"
    mechGun = "mechGun"
    mechMissile = "mechMissile"
    mechBunker = "mechBunker"
    mechBunkerDeployed = "mechBunkerDeployed"
    heavyArtillery = "heavyArtillery"
    bugMeleeLarge = "bugMeleeLarge"
    hovercraft = "hovercraft"
    antiAirTurret = "antiAirTurret"
    c_antiAirTurretT2 = "c_antiAirTurretT2"
    c_antiAirTurretT3 = "c_antiAirTurretT3"
    combatEngineer = "combatEngineer"
    mechEngineer = "mechEngineer"





