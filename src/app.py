from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from view.main_view import MainView
from service.data_rio_parser_service import DataRioParserService
from service.session_state_service import SessionStateService
from view.sidebar_view import SidebarView
from view.settings_view import SettingsView
from view.home_view import HomeView
from view.table_analysis_view import TableAnalysisView


class Container(containers.DeclarativeContainer):    
    data_rio_parser_service = providers.Singleton(DataRioParserService)
    
    session_state_service = providers.Singleton(SessionStateService)
    
    sidebar_view = providers.Singleton(
        SidebarView,
        session_state_service=session_state_service
    )
    
    home_view = providers.Singleton(
        HomeView,
        session_state_service=session_state_service
    )
    
    table_analysis_view = providers.Singleton(
        TableAnalysisView,
        data_rio_parser_service=data_rio_parser_service,
        session_state_service=session_state_service,
        sidebar_view=sidebar_view
    )
    
    settings_view = providers.Singleton(
        SettingsView,
        session_state_service=session_state_service
    )
    
    main_view = providers.Singleton(
        MainView,
        session_state_service=session_state_service,
        sidebar_view=sidebar_view,
        home_view=home_view,
        table_analysis_view=table_analysis_view,
        settings_view=settings_view
    )


@inject
def main(main_view: MainView = Provide[Container.main_view]) -> None:
    main_view.render()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()