package org.dummy.insecure.framework;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.time.LocalDateTime;

public class VulnerableTaskHolder implements Serializable {

        private static final long serialVersionUID = 2;

        private String taskName;
        private String taskAction;
        private LocalDateTime requestedExecutionTime;

        public VulnerableTaskHolder(String taskName, String taskAction) {
                super();
                this.taskName = taskName;
                this.taskAction = taskAction;
                this.requestedExecutionTime = LocalDateTime.now().plusHours(-2);
        }

        private void readObject( ObjectInputStream stream ) throws Exception {
        //deserialize data so taskName and taskAction are available
                stream.defaultReadObject();

                //blindly run some code. #code injection
                Runtime.getRuntime().exec(taskAction);
     }
}