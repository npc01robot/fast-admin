import appTinyGrid from "./src/AppTinyGrid.vue";
import appServerSideGrid from "./src/AppServerSideGrid.vue";
import stGrid from "./src/StGrid.vue";
import { withInstall } from "@pureadmin/utils";

const StGrid = withInstall(stGrid);
const AppTinyGrid = withInstall(appTinyGrid);

const AppServerSideGrid = withInstall(appServerSideGrid);

export { StGrid, AppTinyGrid, AppServerSideGrid };
