import vk_api
from pprint import pprint

def auth_vk():
    vk_session = vk_api.VkApi('', '')
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    return vk_session.get_api()

response = auth_vk().wall.get(owner_id=-40062539, offset=1, count=7)
for i in response['items']:
    print(i['text'])
    for a in i['attachments']:
        if(a['type'] == 'photo'):
            print(a['photo']['sizes'][4]['url'])
        elif(a['type'] == 'video'):
            print(a['video']['description'])
            id_user = a['video']['owner_id']
            id_video = a['video']['id']
            r = auth_vk().video.get(owner_id=-40062539, videos = str(id_user)+'_'+str(id_video))
            for i in r['items']:
                print(i['player'])
