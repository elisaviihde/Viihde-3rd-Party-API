*** Settings ***
Library           ApiElisaViihdeLibrary.py

*** Variables ***
${username} =  FillMeIn
${password} =  FillMeIn
${program_id} =  FillMeIn
${channel_id} =  FillMeIn

${id_token} =           empty
${token} =              empty
${refresh_token} =      empty

${platform_name} =      external
${platform_id} =        1.0

${search_string} =      Down
${include_metadata} =   true

*** Testcases ***
Authenticate Viihde user against OAuth
    ${code} =       Get authcode from OAuth
    ${response} =   Get OAuth token for user with password and code  ${username}  ${password}  ${code}
    Should be equal  ${response.response_type}  token
    Set Global Variable  ${token}  ${response.access_token}
    Set Global Variable  ${refresh_token}  ${response.refresh_token}

Get all recordings for user
    ${response} =  Get all recordings  ${token}  ${platform_name}  ${platform_id}

Get recording info
    ${response} =  Get recording with metadata  ${token}  ${program_id}  ${include_metadata}  ${platform_name}  ${platform_id}

Get recording URL
    ${response} =  Get recording URL  ${token}  ${program_id}  ${platform_name}  ${platform_id}

Get all channels
    ${response} =  Get all channels  ${token}  ${platform_name}  ${platform_id}

Get all EPG info for one channel
    ${response} =  Get schedule for channel with metadata  ${token}  ${channel_id}  ${platform_name}  ${platform_id}

Get program info
    ${response} =  Get program with metadata  ${token}  ${program_id}  ${platform_name}  ${platform_id}

Perform search
    ${response} =  Do search for user  ${token}  ${search_string}  ${include_metadata}  ${platform_name}

