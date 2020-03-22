import * as React from 'react';
import * as Panel from './PlaintextPanel';

import * as API from '../api';
import '../styles/DisplayPanel.css';

interface Props {
    source: string
    children: Array<(state: Panel.PanelProps) => React.ReactNode>
};

interface State {
    data: API.Data,
    activePanelIndex: number,
    panelNames: Array<number>
};

export default class DisplayPanel extends React.Component<Props, State> {

    state = {
        data: [],
        activePanelIndex: 0,
        panelNames: [],
    };

    componentDidMount() {
        this.fetchSource();
        let names = this.props.children.map((panel, idx: number) => {
            console.log(panel.name);
            // return `${idx}:${panel.name}`
            return idx
        })
        this.setState({ panelNames: names})
        console.log(names);
        
    };

    test = (x: string) => {
        return x;
    };

    fetchSource = () => {
        console.log(`Fetching data from: ${this.props.source}`);
        API.get(this.props.source, (data) => {
            console.log(data);
            this.setState({ data: data });
        });
    }

    render() {
        const pprops: Panel.PanelProps = {
            name: 'unnamed',
            data: this.state.data
        };
        return (
            <div className="panelController">
                <div className="controls">
                    <select onChange={(x) => {
                        this.setState({activePanelIndex: Number.parseInt(x.target.value)});
                        // console.log(x.target.value)
                        }}>
                        {this.state.panelNames.map((x) => <option key={x} value={x}>{x}</option>)}
                    </select>
                </div>
                <div className="panelDisplay">
                    {/* {this.props.children.map((x) => x(pprops))} */}
                    {this.props.children[this.state.activePanelIndex](pprops)}
                </div>
            </div>
        );
    }

}
