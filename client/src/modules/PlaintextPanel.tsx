import * as React from 'react';
import * as API from '../api';

export interface PanelProps {
    data: API.Data
    name: string
};

const PlaintextPanel: React.FunctionComponent<PanelProps> = (state) => {
    return (
        <div className="panel">
            {state.data.map((x) => <pre key={`${x.match}:${x.type}`}>{x.type === 'plaintext' ? x.text : null}</pre>
            )}
        </div>
    );
};

export default PlaintextPanel;
