--view to order laps by laptime, enriched by session info
--tracklength clause to account for floating-point error or dropped packets
--considered "close enough" that user probably did a valid lap
create view v_leaderboard as
with
laps as (select
sessionuid,
currentlapnumber as lapnumber,
playercarindex,
min(packettime) as lapstarttime,
max(packettime) as lapendtime,
max(currentlaptime) as laptime,
max(lapdistance) as lapdistance
from gtc_lap_v2
where playerscar = true
group by 1,2,3),
sessions as (select
sessionuid,
trackid,
era,
weather,
max(airtemperature) as airtemp,
max(tracklength) as tracklength,
max(tracktemperature) as tracktemp
from gtc_session_v2
group by 1,2,3,4
)
select
laps.*,
sessions.trackid,
sessions.era,
sessions.weather,
sessions.airtemp,
sessions.tracklength,
sessions.tracktemp
from laps
left join sessions on (laps.sessionuid = sessions.sessionuid)
where lapdistance >= (0.99 * tracklength)
order by laptime;

--view to order laps by laptime, enriched by session info
--where clause trackid = 0 represents Melbourne, Australia
--tracklength clause to account for floating-point error or dropped packets
--considered "close enough" that user probably did a valid lap
create view v_leaderboard_melbourne as
with
laps as (select
sessionuid,
currentlapnumber as lapnumber,
playercarindex,
min(packettime) as lapstarttime,
max(packettime) as lapendtime,
max(currentlaptime) as laptime,
max(lapdistance) as lapdistance
from gtc_lap_v2
where playerscar = true
group by 1,2,3),
sessions as (select
sessionuid,
trackid,
era,
weather,
max(airtemperature) as airtemp,
max(tracklength) as tracklength,
max(tracktemperature) as tracktemp
from gtc_session_v2
group by 1,2,3,4
)
select
laps.*,
sessions.era,
sessions.weather,
sessions.airtemp,
sessions.tracklength,
sessions.tracktemp
from laps
left join sessions on (laps.sessionuid = sessions.sessionuid)
where lapdistance >= (0.99 * tracklength) and trackid = 0
order by laptime

--view to get most recent melbourne lap
--as long as the data pipeline is keeping up, it should be the current lap
create view v_most_recent_lap_melbourne as
with
laps as (select
sessionuid,
currentlapnumber as lapnumber,
playercarindex,
min(packettime) as lapstarttime,
max(packettime) as lapendtime
from gtc_lap_v2
where playerscar = true
group by 1,2,3),
sessions as (select
sessionuid,
trackid
from gtc_session_v2
group by 1,2
)
select
laps.*
from laps
left join sessions on (laps.sessionuid = sessions.sessionuid)
where trackid = 0
order by lapstarttime desc
limit 1
