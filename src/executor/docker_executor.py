class DockerExecutor:
    def __init__(self, docker, docker_image, api_port, submission_port):
        self.docker = docker
        self.docker_image = docker_image
        self.api_port = api_port
        self.submission_port = submission_port

    def create_container(self, submission, container_name, container_command, container_sources):
        try:
            container = self.docker.containers.get(container_name)
        except:
            image = self.docker.images.pull(self.docker_image)
            container_dir = f'/var/builds/{submission}'
            container_volumes = {container_sources: {'bind': container_dir, 'mode': 'rw'}}
            container_env = [f'API_PORT={self.api_port}']
            container = self.docker.containers.create(image, container_command, name=container_name,
                                                      stdin_open=True, tty=True, volumes=container_volumes,
                                                      working_dir=container_dir, environment=container_env,
                                                      ports={f'{self.api_port}/tcp': self.submission_port})
        return DockerContainer(container)


class DockerContainer:
    def __init__(self, container):
        self.container = container

    def run(self):
        self.container.start()
        previous_line = ''
        for line in self.container.attach(stream=True):
            if not line == previous_line:
                print(line.decode('utf-8'))
            previous_line = line
        status = self.container.wait()
        if not status['StatusCode'] == 0:
            raise Exception('Build failed')
