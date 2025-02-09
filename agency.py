from agency_swarm import Agency
from UIDesigner import UIDesigner
from ProjectManager import ProjectManager
from FrontendDeveloper import FrontendDeveloper
from BackendDeveloper import BackendDeveloper

pm = ProjectManager()
frontend = FrontendDeveloper()
backend = BackendDeveloper()
designer = UIDesigner()

agency = Agency([pm, [pm, frontend],
                 [pm, backend],
                 [pm, designer],
                 [frontend, backend],
                 [frontend, designer]],
                shared_instructions='./agency_manifesto.md',
                max_prompt_tokens=25000,
                temperature=0.3)

if __name__ == '__main__':
    agency.demo_gradio()
