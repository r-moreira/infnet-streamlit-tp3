from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from service.streamlit_service import StreamlitService
from view.sidebar_view import SidebarView


class Container(containers.DeclarativeContainer):    
    configuration = providers.Configuration(yaml_files=["./app_config.yaml"])
    
    sidebar_view = providers.Singleton(
        SidebarView
    )
    
    streamlit_service = providers.Singleton(
        StreamlitService,
        sidebar_view=sidebar_view,
        configuration=configuration
    )


@inject
def main(streamlit_service: StreamlitService = Provide[Container.streamlit_service]) -> None:
    streamlit_service.run()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()