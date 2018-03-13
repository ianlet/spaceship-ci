class DockerExecutor:
    def __init__(self, docker, docker_image):
        self.docker = docker
        self.docker_image = docker_image

    def create_container(self, submission, container_name, container_command, container_sources):
        try:
            container = self.docker.containers.get(container_name)
        except:
            image = self.docker.images.pull(self.docker_image)
            container_dir = f'/var/builds/{submission}'
            container_volumes = {container_sources: {'bind': container_dir, 'mode': 'rw'}}
            container = self.docker.containers.create(image, container_command, name=container_name,
                                                      stdin_open=True, tty=True, volumes=container_volumes,
                                                      working_dir=container_dir, links={'mongo': 'mongo'})
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
