from nupic.frameworks.opf.modelfactory import ModelFactory

from model_params.vaccination.vaccine_record_model_params import MODEL_PARAMS
from htmsanity.nupic.runner import SanityRunner
from htmsanity.nupic.model import CLASanityModel

# You create something like this.
class HelloModel(CLASanityModel):
    def __init__(self):
        """MODEL_PARAMS = {
            # Your choice
        }"""
        self.model = ModelFactory.create(MODEL_PARAMS)
        self.lastInput = -1
        super(HelloModel, self).__init__(self.model)

    def step(self):
        self.lastInput = (self.lastInput + 1) % 12
        self.model.run({
            'myInput': self.lastInput,
        })

    def getInputDisplayText(self):
        return {
            'myInput': self.lastInput,
        }

sanityModel = HelloModel()
runner = SanityRunner(sanityModel)
runner.start()