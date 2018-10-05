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
        archiveArtifacts(artifacts: 'dist/tfe_backup-*.tar.gz', onlyIfSuccessful: true)
      }
    }
  }
}