from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, Material, Texture, VBase4
from panda3d.core import GeoMipTerrain, NodePath
from direct.task import Task
import sys

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load texture
        tex = loader.loadTexture("img.jpg")

        # Create sphere
        sphere = self.loader.loadModel("models/sphere")
        sphere.setTexture(tex, 1)
        sphere.reparentTo(self.render)
        sphere.setScale(2)

        # Set up lighting
        self.setupLighting()

        # Spin the sphere
        self.taskMgr.add(self.spinSphere, "SpinSphere")

    def setupLighting(self):
        # Ambient light
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        ambientLightNP = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNP)

        # Directional light
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setColor(VBase4(0.8, 0.8, 0.8, 1))
        directionalLightNP = self.render.attachNewNode(directionalLight)
        directionalLightNP.setHpr(45, -45, 0)
        self.render.setLight(directionalLightNP)

    def spinSphere(self, task):
        dt = globalClock.getDt()
        angle_degrees = 20.0 * dt
        self.render.setH(self.render, angle_degrees)
        return Task.cont

app = MyApp()
app.run()
