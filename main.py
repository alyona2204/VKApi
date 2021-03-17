import requests
import time

with open('token.txt') as file_object:
    token = file_object.read().strip()

class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token: str, version: str):
        self.token = token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def photo(self):
        try:
            id = input('Введите id пользователя VK: ')
            tokenYA = input('Введите token с Полигона Яндекс.Диска: ')
            self.params = {
                'user_ids': id,
                'owner_id': id,
                'access_token': self.token,
                'v': self.version,
                'album_id': 'profile',
                'extended': 1
            }

            res = requests.get(self.url + 'photos.get', self.params).json()
            profile = requests.get(self.url + 'users.get', self.params).json()
            for el in profile['response']:
                first_name = el['first_name']
                last_name = el['last_name']
            profile_name = f'{first_name} {last_name}'
            param_photo = res['response']['items']
            info = []
            for element in param_photo:
                param_size = element['sizes']
                size = param_size[-1]
                param_likes = element['likes']['count']
                date = element['date']
                file_name = (str(param_likes) + ' ' + str(date) + '.jpg')
                new = {'file_name': file_name, 'type': size['type']}
                info.append(new)
                file_path = requests.get(size['url'])

                name = (str(profile_name)+'/'+ file_name)
                res = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                   params={'path': profile_name},
                                   headers={'Authorization': 'OAuth ' + tokenYA})
                resp = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                        params={'path': name},
                                        headers={'Authorization': 'OAuth ' + tokenYA})

                with open("logs.json", "a") as f:
                    print(time.strftime('%x, %X'), name, resp.status_code, resp.json(), file=f)
                href = resp.json()['href']
                resp = requests.put(href, file_path.content)
                percent = 100/335
                progress = 0
                for buf in range(335):
                    progress += percent
                    print(f'\rОбработка файла {file_name} завершена на %3d%%' % progress, end='', flush=True)
                    time.sleep(0.01)

            print(' Файлы успешно загружены')
        except Exception as e:
            print("Error! " + str(e))
            print(vk_client.photo())

        with open("info_photos.json", "a") as f:
            print(info, file=f)

vk_client = VkUser(token, '5.126')
print(vk_client.owner_id)
vk_client.photo()