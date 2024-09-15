from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from service.streamlit_service import StreamlitService
from service.datario_parser_service import DataRioParserService
from view.sidebar_view import SidebarView


class Container(containers.DeclarativeContainer):    
    configuration = providers.Configuration(yaml_files=["./app_config.yaml"])
    
    data_rio_parser_service = providers.Singleton(
        DataRioParserService
    )
    
    sidebar_view = providers.Singleton(
        SidebarView
    )
    
    streamlit_service = providers.Singleton(
        StreamlitService,
        configuration=configuration,
        data_rio_parser_service=data_rio_parser_service,
        sidebar_view=sidebar_view,
    )


@inject
def main(streamlit_service: StreamlitService = Provide[Container.streamlit_service]) -> None:
    streamlit_service.run()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()