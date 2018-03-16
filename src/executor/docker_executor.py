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
        return DockerContainer(container, container_name)


class DockerContainer:
    def __init__(self, container, container_name):
        self.container = container
        self.container_name = container_name

    def run(self):
        self.container.start()
        status = self.container.wait()
        if not status['StatusCode'] == 0:
            raise Exception(f'{self.container_name} failed')
