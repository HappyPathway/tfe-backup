pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'python2.7 setup.py sdist bdist_wheel'
      }
    }
    stage('Publish') {
      steps {
        archiveArtifacts(artifacts: 'tfe_backup-*.tar.gz', onlyIfSuccessful: true)
      }
    }
  }
}