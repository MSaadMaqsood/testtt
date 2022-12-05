import { React, Component } from "react";
import "../../global/style/style.css";


class Exe_Dashboard extends Component {
    constructor(props) {
      super(props);
      this.state = {
        street_health: 0,
        green_index: 0,
        risk: 0,
        data_map: {'line':[],'circle':[]},
        tree_map: {'line':[],'circle':[]},
        render: true,
      };
    }

    render() {
        return (<div>
                <div>Executive Dashboard</div>
        </div>);
    }
}
export default Exe_Dashboard;