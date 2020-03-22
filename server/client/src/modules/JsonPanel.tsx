import * as React from 'react';
import * as API from '../api';

export interface PanelProps {
    data: API.Data
    name: string
};

const JsonPanel: React.FunctionComponent<PanelProps> = (state) => {
    return (
        <div className="panel">
            <pre>
                {JSON.stringify(state.data, null, 4)}
            </pre>
        </div>
    );
};

export default JsonPanel;
