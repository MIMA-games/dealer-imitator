def buildImage() {
    echo "Starting application build"
    withCredentials([file(credentialsId: 'jenkins-gcr-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
        sh 'docker login -u _json_key -p "`cat ${GOOGLE_APPLICATION_CREDENTIALS}`" https://gcr.io'
        sh 'docker build -f src/Dockerfile ./src -t dealer-imitator:dev --build-arg GROUP_ID=1000 --build-arg USER_ID=1000'
    }
}

def securityScan() {
    echo "Starting security scan"
    withCredentials([file(credentialsId: 'jenkins-gcr-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
        sh """
            docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp aquasec/trivy  --exit-code 1 --severity CRITICAL image dealer-imitator:dev
        """
    }
}

def TestApp() {
    echo "Starting unit test"

    try {
        // Check if network exists
        sh 'docker network inspect mima_network'
    } catch (Exception e) {
        // Create network if it does not exist
        sh 'docker network create mima_network'
    }

    sh 'docker-compose -f docker-compose.yml up --build -d && docker-compose exec -T dealer-imitator-srv pytest -s -vv &&  docker-compose -f docker-compose.yml down'

    // Remove network after tests have completed
    sh 'docker network rm mima_network'

    return 0 // Explicitly specify exit code 
}

def pushImage() {
    echo "Pushing image to GCR"
    withCredentials([file(credentialsId: 'jenkins-gcr-account', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
        sh 'docker tag dealer-imitator:dev gcr.io/mima-325516/dealer-imitator/dealer-imitator:dev'
        sh 'docker push gcr.io/mima-325516/dealer-imitator/dealer-imitator:dev'
    }
}

def deployToDev() {
    sh 'echo "starting deployment"'
    sh 'helm upgrade --install --atomic --wait dealer-imitator deployment \
    --set image.releaseDate=VRSN`date +%Y%m%d-%H%M%S` \
    -n dev'
    echo "App deployed to dev env"
}
return this
