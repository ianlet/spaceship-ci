import os
import shutil

from git import Repo


class Assignment:
    ASSIGNMENT_IMAGE = 'gradle:4.5.1-jdk8'
    ASSIGNMENT_PORT = 5000

    def __init__(self, docker, name, url):
        self.docker = docker
        self.name = name
        self.url = url

    def clone_or_update(self, base_path):
        path = f'{base_path}/{self.name}'

        if os.path.exists(path):
            print(f'Assignment {self.name} already exists at {path}')
            self.__clear(path)

        self.__clone(path)

    def __clone(self, path):
        print(f'Cloning assignment {self.name} into {path}...')
        assignment_repo = Repo.clone_from(self.url, path)
        print(f'Assignment cloned!')

        print(f'Checking out {self.name} to master...')
        assignment_repo.heads.master.checkout()

    def __clear(self, path):
        print(f'Clearing {path}...')
        shutil.rmtree(path)
        print(f'Assignment cleared!')

    def build(self, source_path):
        print(f'Building assignment {self.name}...')
        container_name = f'{self.name}--build'
        container_command = ['./gradlew', 'build', '-x', 'test']
        container = self.__create_or_get_container(container_name, container_command, source_path)
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

    def __create_or_get_container(self, container_name, container_command, source_path):
        try:
            return self.docker.containers.get(container_name)
        except:
            return self.__create_container(container_name, container_command, source_path)

    def __create_container(self, container_name, container_command, source_path):
        print(f'Pulling image {self.ASSIGNMENT_IMAGE}...')
        image = self.docker.images.pull(self.ASSIGNMENT_IMAGE)

        print(f'Creating container {container_name} on {self.ASSIGNMENT_IMAGE}')
        container_sources = f'{source_path}/{self.name}'
        container_volumes = {container_sources: {'bind': f'/var/builds/{self.name}', 'mode': 'rw'}}
        container_working_dir = f'/var/builds/{self.name}'
        container = self.docker.containers.create(image, container_command, name=container_name,
                                                  stdin_open=True, tty=True, volumes=container_volumes,
                                                  working_dir=container_working_dir,
                                                  ports={'1357/tcp': self.ASSIGNMENT_PORT})
        print(f'Container {container.name} created!')
        return container

    def test(self, source_path):
        print(f'Testing assignment {self.name}...')
        container_name = f'{self.name}--test'
        container_command = ['./gradlew', 'test']
        container = self.__create_or_get_container(container_name, container_command, source_path)
        status = self.__start_container_and_wait(container)
        if not status['StatusCode'] == 0:
            raise Exception('Test failed')

    def evaluate_progress(self, source_path):
        print(f'Evaluating progress of assignment {self.name}...')
        container_name = f'{self.name}--run'
        container_command = ['./gradlew', 'run']
        container = self.__create_or_get_container(container_name, container_command, source_path)
        self.__ensure_started(container)
        # retrieve the test cases and run them one by one to track the progress

    def __ensure_started(self, container):
        container.start()
        # add a heartbeat in the boilerplate and ping it until it is up and running to ensure container is started
