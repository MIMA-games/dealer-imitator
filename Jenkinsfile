def gv

pipeline {
    agent { label 'builder' }
    environment {
        SERVER_CREDENTIALS = credentials('jenkins-gcr-account')
    }
    stages {
        stage('Load script') {
            steps {
                script {
                    gv = load 'script.groovy'
                    env.GIT_COMMIT_MSG = sh(script: 'git log -1 --pretty=%B ${GIT_COMMIT} | head -n1', returnStdout: true).stripIndent().trim()
                    env.GIT_AUTHOR = sh(script: 'git log -1 --pretty=%ae ${GIT_COMMIT} | awk -F "@" \'{print $1}\' | grep -Po "[a-z]{1,}" | head -n1', returnStdout: true).trim()
                }
            }
        }
        stage('Build Image') {
            when {
                allOf {
                    branch 'master'
                    not {
                        changeRequest()
                    }
                }
            }
            steps {
                slackSend(color: '#00FF00', message: "build - ${env.BUILD_NUMBER} ${env.JOB_NAME} Started  ${env.BUILD_NUMBER}  by changes from ${env.GIT_AUTHOR} commit message ${env.GIT_COMMIT_MSG} (<${env.BUILD_URL}|Open>)")
                script {
                    gv.buildImage()
                }
            }
        }
        stage('Pull Request Build') {
            when {
                allOf {
                    not {
                        branch 'master'
                    }
                    changeRequest()
                }
            }
            steps {
                script {
                    git branch: "${CHANGE_TARGET}", changelog: false, poll: false, 
                     url: "${env.CHANGE_URL}"
                    sh 'git checkout FETCH_HEAD'
                    gv.buildImage()
                    gv.securityScan()
                }
            }
            post {
                success {
                    slackSend(color: '#00FF00', message: "Pull Request Build successful - ${env.BUILD_NUMBER} by changes from ${env.CHANGE_AUTHOR_DISPLAY_NAME} (<${env.BUILD_URL}|Open>)")
                }
                failure {
                    slackSend(color: '#FF0000', message: "Pull Request Build failed - ${env.BUILD_NUMBER} by changes from ${env.CHANGE_AUTHOR_DISPLAY_NAME} (<${env.BUILD_URL}|Open>)")
                }
            }
        }
        stage('Security scan') {
            when {
                branch 'master'
            }
            steps {
                slackSend(color: '#00FF00', message: "Security scan - ${env.BUILD_NUMBER} ${env.JOB_NAME} Started  ${env.BUILD_NUMBER}  by changes from ${env.GIT_AUTHOR} commit message ${env.GIT_COMMIT_MSG} (<${env.BUILD_URL}|Open>)")
                script {
                    gv.securityScan()
                }
            }
        }
        stage('Unit test') {
            when {
                branch 'master'
            }
            steps {
                slackSend(color: '#00FF00', message: "Security scan - ${env.BUILD_NUMBER} ${env.JOB_NAME} Started  ${env.BUILD_NUMBER}  by changes from ${env.GIT_AUTHOR} commit message ${env.GIT_COMMIT_MSG} (<${env.BUILD_URL}|Open>)")
                script {
                    gv.TestApp()
                }
            }            
        }
        stage('Push image to repo') {
            when {
                allOf {
                    branch 'master'
                    not {
                        changeRequest()
                    }
                }
            }
            steps {
                slackSend(color: '#00FF00', message: "Push image to repo  - ${env.BUILD_NUMBER} ${env.JOB_NAME} Started  ${env.BUILD_NUMBER} for user: ${env.GIT_AUTHOR} commit message ${env.GIT_COMMIT_MSG} (<${env.BUILD_URL}|Open>)")
                script {
                    gv.pushImage()
                }
            }
        }
        stage('Deploy for dev and Q/A') {
            agent { label 'master' }
            when {
                branch 'master'
            }
            steps {
                script {
                    gv.deployToDev()
                }
            }
        }
    }
    post {
        success {
            slackSend(color: '#00FF00', message: "Success  job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.BUILD_URL}|Open>)")
        }
        failure {
            slackSend(color: '#FF0000', message: "Failed: job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (<${env.BUILD_URL}|Open>)")
        }
    }
}
