from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException, Query
import pytz

app = FastAPI()

# --------------------------------------------------------------------------
# Human-readable description of formats for the /time/formats endpoint
#
# We include the " - (default)" suffix for the first one to indicate that
# it's used if no format parameter is provided.
# --------------------------------------------------------------------------
FORMATS_LIST = [
    "YYYY-MM-DD HH:mm:ss - (default)",
    "YYYY-MM-DDTHH:mm:ssZ (ISO-8601)",
    "Mon, 02 Jan 2006 15:04:05 MST (RFC-2822)"
]

# --------------------------------------------------------------------------
# Internal mapping from short keys -> actual formatting logic.
#
# We keep these keys short (e.g., "default", "iso-8601", "rfc-2822") so
# we don't have to worry about URL encoding.
# --------------------------------------------------------------------------

def default_format(dt: datetime) -> str:
        """Return a string in YYYY-MM-DD HH:mm:ss format."""
        return dt.strftime("%Y-%m-%d %H:%M:%S")

def iso_8601_format(dt: datetime) -> str:
        """Return an ISO-8601 style UTC string, appending 'Z' for clarity."""
        utc_dt = dt.astimezone(pytz.UTC)
        return utc_dt.isoformat() + "Z"


def rfc_2822_format(dt: datetime) -> str:
    """Return a string in RFC-2822 style."""
    return dt.strftime("%a, %d %b %Y %H:%M:%S %Z")    

FORMAT_MAPPINGS = {
    "default": default_format,
    "iso-8601": iso_8601_format,
    "rfc-2822": rfc_2822_format
}

# For quick reference:
#   default   -> "YYYY-MM-DD HH:mm:ss"
#   iso-8601  -> "YYYY-MM-DDTHH:mm:ssZ (ISO-8601)"
#   rfc-2822  -> "Mon, 02 Jan 2006 15:04:05 MST (RFC-2822)"




# --------------------------------------------------------------------------
# 1. /time/formats
#    Return the list of format descriptions (including the default indicator).
# --------------------------------------------------------------------------
@app.get("/time/formats", response_model=List[str])
def get_time_formats():
    return FORMATS_LIST

# --------------------------------------------------------------------------
# 2. /time/current
#    Accept an optional 'format' parameter. If not provided, use 'default'.
# --------------------------------------------------------------------------
@app.get("/time/current")
def current_time(format: str = Query(None)):
      
    # If no format param, default to "default"    
    if format is None:
        format = "default"

    format = format.lower()  # make it case-insensitive if desired
    if format not in FORMAT_MAPPINGS:
        raise HTTPException(status_code=400, detail=f"Unsupported format identifier: {format}")
    
    now_local = datetime.now()
    formatted_time = FORMAT_MAPPINGS[format](now_local) 

    return {
        "currentTime": formatted_time,
        "format": format         
    }

# --------------------------------------------------------------------------
# 3. /timezones
#    List commonly used time zones
# --------------------------------------------------------------------------
@app.get("/timezones")
def get_timezones():
    """
    Returns a list of commonly used time zones (from pytz).
    """
    return list(pytz.common_timezones)      

# --------------------------------------------------------------------------
# 4. /time/zone
#    Provide current time for a specified time zone (optional format).
# --------------------------------------------------------------------------
@app.get("/time/zone")
def get_time_for_timezone(
    tz: str,
    format:str = Query(None)):
    """
    If tz is unsupported, return 400 with "<tz> is not supported".
    If 'format' is missing or invalid, use 'default' or return 400, respectively.
    """     

    # Validate timezone
    if tz not in pytz.common_timezones:
        raise HTTPException(status_code=400, detail=f"{tz} is not supported")
    
    # If no format param, default to "default"    
    if format is None:
        format = "default"
    format = format.lower()

    if format not in FORMAT_MAPPINGS:
        raise HTTPException(status_code=400, detail=f"Unsupported format identifier: {format}")
    
    timezone_obj = pytz.timezone(tz)
    now_in_tz = datetime.now(timezone_obj)
    formatted_time = FORMAT_MAPPINGS[format](now_in_tz)

    return {
        "currentTime": formatted_time,
        "requestedTimeZone": tz,
        "format": format                
    }
