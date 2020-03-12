import vk_api
import config
from config import channels


def auth_vk():
    vk_session = vk_api.VkApi(config.login, config.password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    return vk_session.get_api()


def get_posts_from_channel(channel: int, count: int) -> list:
    response = auth_vk().wall.get(owner_id=channel, offset=1, count=count)
    data_list = []
    data = {}
    for i in response['items']:
        data['text'] = i['text']
        data['photo'] = []
        data['video'] = []
        for a in i['attachments']:
            if(a['type'] == 'photo'):
                data['photo'].append(a['photo']['sizes'][4]['url'])
            elif(a['type'] == 'video'):
                data['video'].append(a['video']['description'])
                id_user = a['video']['owner_id']
                id_video = a['video']['id']
                r = auth_vk().video.get(owner_id=channels[0], videos = str(id_user)+'_'+str(id_video))
                for i in r['items']:
                    data['video'].append(i['player'])
        data_list.append(data)
    return data_list


if __name__ == "__main__":
    post = get_posts_from_channel(channels[0], 1)
    print(post)