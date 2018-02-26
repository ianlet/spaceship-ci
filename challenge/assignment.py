import os

from git import Repo


class Assignment:
    def __init__(self, docker, name, url):
        self.docker = docker
        self.name = name
        self.url = url

    def clone_or_update(self, base_path):
        path = f'{base_path}/{self.name}'
        if os.path.exists(path):
            print(f'Assignment {self.name} already exists at {path}')
            self.__update(path)
        else:
            self.__clone(path)

    def __clone(self, path):
        print(f'Cloning assignment {self.name} into {path}...')
        assignment_repo = Repo.clone_from(self.url, path)
        print(f'Assignment cloned!')

        print(f'Checking out {self.name} to master...')
        assignment_repo.heads.master.checkout()

    def __update(self, path):
        print(f'Checking out {self.name} to master...')
        assignment_repo = Repo(path)
        assignment_repo.heads.master.checkout()

        print(f'Updating assignment {self.name}...')
        origin = assignment_repo.remote('origin')
        origin.pull(['--ff', '--force'])

        print(f'Assignment updated!')

    def build(self, source_path):
        print(f'Building assignment {self.name}...')
        container_name = f'{self.name}--build'
        container = self.__create_or_get_container(container_name, source_path)
        status = self.__start_container_and_wait(container)
        if not status['StatusCode'] == 0:
            raise Exception('Build failed')

    def __start_container_and_wait(self, container):
        container.start()
        previous_line = ''
        for line in container.attach(stream=True):
            if not line == previous_line:
                print(line.decode('utf-8'))
            previous_line = line
        status = container.wait()
        return status

    def __create_or_get_container(self, container_name, source_path):
        try:
            return self.docker.containers.get(container_name)
        except:
            return self.__create_container(container_name, source_path)

    def __create_container(self, container_name, source_path):
        image_name = 'gradle:4.5.1-jdk8'
        print(f'Pulling image {image_name}...')
        image = self.docker.images.pull(image_name)

        print(f'Creating container {container_name} on {image_name} bound to {source_path}')
        container_sources = f'{source_path}/{self.name}'
        container_command = ['./gradlew', 'build', '-x', 'test']
        container_volumes = {container_sources: {'bind': f'/var/builds/{self.name}', 'mode': 'rw'}}
        container_working_dir = f'/var/builds/{self.name}'
        container = self.docker.containers.create(image, container_command, name=container_name,
                                                  stdin_open=True, tty=True, volumes=container_volumes,
                                                  working_dir=container_working_dir)
        print(f'Container {container.name} created!')
        return container
