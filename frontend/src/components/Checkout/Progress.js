import { Box, Step, StepLabel, Stepper } from '@mui/material';

import React from 'react';

export default function Progress({ steps, activeStep }) {

    return (
        <div style={{ "marginTop": "30px"}}>
            <Box sx={{ width: '100%' }}>
                <Stepper activeStep={activeStep} alternativeLabel>
                    {
                        steps.map((label, index) => {
                            const stepProps = {};
                            const labelProps = {};
                            return (
                                <Step key={index} {...stepProps}>
                                    <StepLabel {...labelProps}>{label}</StepLabel>
                                </Step>
                            );
                        })
                    }
                </Stepper>
            </Box>
        </div>

    );
}
